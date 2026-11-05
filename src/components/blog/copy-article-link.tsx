"use client";
import {useState} from "react";
export default function CopyArticleLink(){const [copied,setCopied]=useState(false);return <button className="ref-copy" type="button" onClick={async()=>{try{await navigator.clipboard.writeText(window.location.href);setCopied(true);window.setTimeout(()=>setCopied(false),1800)}catch{setCopied(false)}}}>{copied?"ENLACE COPIADO ✓":"COPIAR ENLACE ↗"}</button>}
