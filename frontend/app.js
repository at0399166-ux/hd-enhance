let type="image"; const file=document.getElementById("file");
document.querySelectorAll(".tab").forEach(b=>b.onclick=()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active")); b.classList.add("active");
  type=b.dataset.type; file.value=""; file.accept=type==="image"?"image/*":"video/*";
  document.getElementById("fileInfo").classList.add("hidden"); document.getElementById("download").classList.add("hidden");
  document.getElementById("enhance").disabled=true; document.getElementById("status").textContent="";
});
file.onchange=()=>{
  const f=file.files[0]; if(!f)return;
  const info=document.getElementById("fileInfo"); info.textContent=`${f.name} • ${(f.size/1024/1024).toFixed(1)} MB`;
  info.classList.remove("hidden"); document.getElementById("enhance").disabled=false;
};
document.getElementById("enhance").onclick=async()=>{
  const f=file.files[0]; if(!f)return;
  const status=document.getElementById("status"), btn=document.getElementById("enhance");
  btn.disabled=true; status.textContent="Processing… please wait";
  document.getElementById("download").classList.add("hidden");
  const fd=new FormData(); fd.append("file",f); fd.append("scale",document.getElementById("scale").value);
  fd.append("sharpen",document.getElementById("sharpen").value); fd.append("denoise",document.getElementById("denoise").checked?"1":"0");
  try{
    const r=await fetch(type==="image"?"/api/enhance/image":"/api/enhance/video",{method:"POST",body:fd});
    const data=await r.json(); if(!r.ok) throw new Error(data.detail||"Enhancement failed");
    const a=document.getElementById("download"); a.href=data.download; a.classList.remove("hidden"); status.textContent="✅ Enhancement complete!";
  }catch(e){status.textContent="❌ "+e.message}
  btn.disabled=false;
};