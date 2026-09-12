import type {ChatResponse} from "../types/chat";
const API_URL=import.meta.env.VITE_API_URL||"http://localhost:8000";
export async function sendChat(payload:{message:string;language:string;location?:string;crop?:string;soil_type?:string;irrigation?:string}):Promise<ChatResponse>{
  const r=await fetch(`${API_URL}/api/v1/chat`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
  const data=await r.json(); if(!r.ok) throw new Error(data.detail||"Unable to reach KrishiNiti AI."); return data;
}
