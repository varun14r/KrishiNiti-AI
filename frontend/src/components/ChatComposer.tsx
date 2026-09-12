import {Send,MapPin} from "lucide-react";import{useState}from"react";
export function ChatComposer({onSend,loading}:{onSend:(text:string)=>void;loading:boolean}){
 const[text,setText]=useState("");const submit=()=>{const v=text.trim();if(!v||loading)return;onSend(v);setText("")};
 return <div className="composer-wrap"><div className="composer"><textarea value={text} onChange={e=>setText(e.target.value)} onKeyDown={e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();submit()}}} placeholder="Ask about crops, soil, irrigation, pests, weather or mandi information..." rows={2}/><button onClick={submit} disabled={loading||!text.trim()}><Send size={18}/></button></div><div className="composer-hint"><span><MapPin size={13}/> Add location or crop details for better recommendations</span><span>Enter to send · Shift+Enter for new line</span></div></div>
}
