"use client";
import Link from "next/link";
import {useEffect,useState} from "react";
export default function ReferenceNav(){
 const [open,setOpen]=useState(false),[clock,setClock]=useState("--:--"),[solid,setSolid]=useState(false);
 useEffect(()=>{const tick=()=>setClock(new Date().toLocaleTimeString("es-ES",{hour:"2-digit",minute:"2-digit"}));tick();const timer=window.setInterval(tick,20000);const scroll=()=>setSolid(window.scrollY>80);window.addEventListener("scroll",scroll,{passive:true});return()=>{window.clearInterval(timer);window.removeEventListener("scroll",scroll)}},[]);
 useEffect(()=>{document.documentElement.classList.add("js");document.body.style.overflow=open?"hidden":"";return()=>{document.body.style.overflow=""}},[open]);
 const links=[["/#manifiesto","Enfoque","Cómo pienso"],["/#proyectos","Proyectos","Trabajo y experimentos"],["/#hago","Qué hago","Desarrollo y diseño"],["/#formacion","Formación","Aprendizaje"],["/blog","Blog","Ideas y artículos"],["/#contacto","Contacto","Hablemos"]];
 return <><header className={`ref-header ${solid&&!open?"solid":""}`}><Link href="/" className="brand">Nil Blanch</Link><div className="hmid"><span>Desarrollo web y software</span><span>{clock}</span></div><button className="idx" aria-expanded={open} aria-controls="ref-overlay" onClick={()=>setOpen(!open)}><span>{open?"Cerrar":"Índice"}</span><i/></button></header><nav id="ref-overlay" className={`ref-overlay ${open?"open":""}`} aria-label="Navegación principal" aria-hidden={!open}><ul>{links.map(([href,label,detail])=><li key={href}><Link href={href} onClick={()=>setOpen(false)}>{label}<span>{detail}</span></Link></li>)}</ul><p className="mono">Software propio. Datos bajo tu control.</p></nav></>;
}
