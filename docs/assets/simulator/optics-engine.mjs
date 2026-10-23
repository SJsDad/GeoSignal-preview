/** Scalar optics shared by UI/worker, checked against NumPy.
 * u = vacuum wavelength * frequency; lengths in wafer-side um.
 * inverted=true evaluates the actual 4f wafer coordinate x/P.
 */
export const FOCAL_UM = 10000;
export const NX = 600;
export const NZ = 101;
const EPS = 16 * Number.EPSILON;
const TAU = 2 * Math.PI;
export function coefficient(order, duty) {
  const argument = Math.PI * order * duty;
  return Math.abs(argument) < 1e-14 ? duty : duty * Math.sin(argument) / argument;
}
export function phaseRate(u, wavelengthUm, model) {
  return model === 'paraxial' ? -Math.PI*u*u/wavelengthUm :
    TAU/wavelengthUm * (Math.sqrt(Math.max(0,1-u*u))-1);
}
export function prepareGrating(config) {
  const wavelengthUm=config.wavelength_nm/1000, u0=config.wavelength_nm/config.pitch_nm;
  const spectrum=[], active=[];
  for (let j=-config.max_order;j<=config.max_order;j++) {
    const u=config.source_u+j*u0, c=coefficient(j,config.duty_ratio), passed=Math.abs(u)<=config.na+EPS;
    const s={order:j,u,coefficient:c,passed,nonzero:passed&&Math.abs(c)>1e-12,rate:phaseRate(u,wavelengthUm,config.phase_model)};
    spectrum.push(s);if(passed) active.push(s);
  }
  const x=Float64Array.from({length:NX},(_,k)=>-1.5+3*k/NX);
  const real=new Float64Array(active.length*NX), imag=new Float64Array(real.length);
  const contrastReal=new Float64Array(active.length*1024), contrastImag=new Float64Array(contrastReal.length);
  active.forEach((s,i)=>{
    for(let k=0;k<NX;k++){real[i*NX+k]=Math.cos(TAU*s.order*x[k]);imag[i*NX+k]=Math.sin(TAU*s.order*x[k]);}
    for(let k=0;k<1024;k++){contrastReal[i*1024+k]=Math.cos(TAU*s.order*k/1024);contrastImag[i*1024+k]=Math.sin(TAU*s.order*k/1024);}
  });
  const omitted=[];
  const first=Math.ceil((-config.na-config.source_u)/u0-EPS), last=Math.floor((config.na-config.source_u)/u0+EPS);
  for(let j=first;j<=last;j++) if(Math.abs(j)>config.max_order&&Math.abs(coefficient(j,config.duty_ratio))>1e-12) omitted.push(j);
  const mask=Float64Array.from(x,v=>config.duty_ratio===1||Math.abs(((v+.5)%1+1)%1-.5)<config.duty_ratio/2?1:0);
  return {config,wavelengthUm,u0,spectrum,active,x,mask,real,imag,contrastReal,contrastImag,omitted};
}
function field(prepared,focus,count,real,imag,inverted) {
  const re=new Float64Array(count),im=new Float64Array(count), sign=inverted?-1:1;
  prepared.active.forEach((s,index)=>{
    const phi=s.rate*focus,a=s.coefficient*Math.cos(phi),b=s.coefficient*Math.sin(phi),offset=index*count;
    for(let k=0;k<count;k++){const c=real[offset+k],d=sign*imag[offset+k];re[k]+=a*c-b*d;im[k]+=a*d+b*c;}
  });
  return {intensity:Float64Array.from(re,(a,k)=>a*a+im[k]*im[k]),re,im};
}
export function evaluateImage(prepared,focus,inverted=false) {
  const image=field(prepared,focus,NX,prepared.real,prepared.imag,inverted);
  const period=field(prepared,focus,1024,prepared.contrastReal,prepared.contrastImag,inverted).intensity;
  let maximum=0,minimum=Infinity;
  for(const v of period){maximum=Math.max(maximum,v);minimum=Math.min(minimum,v);}
  const spectrum=prepared.spectrum.map(s=>({...s,total_phase_pi:s.nonzero?Math.atan2(s.coefficient*Math.sin(s.rate*focus),s.coefficient*Math.cos(s.rate*focus))/Math.PI:null}));
  return {...image,x_over_pitch:prepared.x,mask:prepared.mask,spectrum,
    active_orders:spectrum.filter(s=>s.nonzero).map(s=>s.order),omitted_orders:prepared.omitted,
    contrast:maximum+minimum>1e-14?(maximum-minimum)/(maximum+minimum):0,
    source_angle_deg:Math.asin(prepared.config.source_u)*180/Math.PI,u0:prepared.u0,focus_um:focus,
    phase_model:prepared.config.phase_model,maximum_bound:prepared.active.reduce((sum,s)=>sum+Math.abs(s.coefficient),0)**2};
}
export function evaluateSweep(prepared,inverted=false) {
  const values=new Float64Array(NX*NZ);let maximum=0;
  for(let row=0;row<NZ;row++){
    const intensity=field(prepared,-1+2*row/(NZ-1),NX,prepared.real,prepared.imag,inverted).intensity;
    values.set(intensity,row*NX);for(const value of intensity) maximum=Math.max(maximum,value);
  }
  return {values,maximum,rows:NZ,columns:NX};
}
/** Equal-focal-length ideal thin lenses; h and z in units of f.
 * The condenser gives slope u_s; diffraction sets u_j; 4f gives h_image=-h_mask.
 */
export function traceSixF(sourceU,orderU,maskHeight,focusUm=0) {
  const dz=focusUm/FOCAL_UM;
  return [
    {plane:'source',z:0,h:-sourceU,slope:maskHeight},
    {plane:'condenser',z:1,h:maskHeight-sourceU,slope:sourceU},
    {plane:'mask',z:2,h:maskHeight,slope:orderU},
    {plane:'objective',z:3,h:maskHeight+orderU,slope:-maskHeight},
    {plane:'pupil',z:4,h:orderU,slope:-maskHeight},
    {plane:'tube',z:5,h:orderU-maskHeight,slope:-orderU},
    {plane:'wafer',z:6+dz,h:-maskHeight-dz*orderU,slope:-orderU},
  ];
}
