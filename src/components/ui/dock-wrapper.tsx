"use client";
import {usePathname} from "next/navigation";
import {Dock} from "./dock";
export const DockWrapper=()=>usePathname()==="/" ? <Dock/> : null;
