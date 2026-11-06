"use client";
import Link from "next/link";
import {Home,Briefcase,Award,PenTool,Mail} from "lucide-react";
const items=[{icon:Home,label:"Inicio",href:"/#inicio"},{icon:Briefcase,label:"Proyectos",href:"/#proyectos"},{icon:Award,label:"Formación",href:"/#formacion"},{icon:PenTool,label:"Blog",href:"/#hblog"},{icon:Mail,label:"Contacto",href:"/#contacto"}];
export const Dock=()=> <nav aria-label="Accesos rápidos" className="ref-dock">{items.map(({icon:Icon,label,href})=><Link key={label} href={href} aria-label={label} title={label}><Icon size={18}/><span>{label}</span></Link>)}</nav>;
