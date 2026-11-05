"use client";
import {useEffect,useState} from "react";
type Heading={level:number;text:string;id:string};
export default function ReferenceToc({headings}:{headings:Heading[]}){
 const [active,setActive]=useState(headings[0]?.id||"");
 useEffect(()=>{const els=headings.map(h=>document.getElementById(h.id)).filter((e):e is HTMLElement=>!!e);if(!els.length)return;const observer=new IntersectionObserver(entries=>{const visible=entries.filter(e=>e.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top);if(visible[0])setActive(visible[0].target.id)},{rootMargin:"-18% 0px -68% 0px",threshold:[0,.1,.5,1]});els.forEach(el=>observer.observe(el));const update=()=>{let current=els[0];for(const el of els){if(el.getBoundingClientRect().top<window.innerHeight*.32)current=el;else break}setActive(current.id)};window.addEventListener("scroll",update,{passive:true});update();return()=>{observer.disconnect();window.removeEventListener("scroll",update)}},[headings]);
 return <aside className="toc"><span className="mono">EN ESTE ARTÍCULO</span><nav aria-label="Índice del artículo">{headings.map(h=><a key={h.id} href={`#${h.id}`} className={active===h.id?"on":""} data-level={h.level}>{h.text}</a>)}</nav></aside>;
}
