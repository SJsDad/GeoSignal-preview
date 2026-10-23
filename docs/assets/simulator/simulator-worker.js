import {prepareGrating,evaluateSweep} from './optics-engine.mjs';
const colors=[[0,0,4],[66,10,104],[147,38,103],[221,81,58],[252,165,10],[252,255,164]];
self.onmessage=({data:{key,config}})=>{
  try {
    const map=evaluateSweep(prepareGrating(config),true),pixels=new Uint8ClampedArray(map.rows*map.columns*4);
    for(let y=0;y<map.rows;y++)for(let x=0;x<map.columns;x++){
      const v=map.values[(map.rows-y-1)*map.columns+x]/Math.max(1e-12,map.maximum)*(colors.length-1);
      const i=Math.min(colors.length-2,Math.floor(v)),f=v-i,offset=(y*map.columns+x)*4;
      for(let c=0;c<3;c++)pixels[offset+c]=colors[i][c]*(1-f)+colors[i+1][c]*f;
      pixels[offset+3]=255;
    }
    self.postMessage({key,maximum:map.maximum,rows:map.rows,columns:map.columns,pixels:pixels.buffer},[pixels.buffer]);
  }catch(error){self.postMessage({key,error:error.message});}
};
