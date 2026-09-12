import type {ChatResponse} from "../types/chat";
export function MessageBubble({message,result}:{message:string;result?:ChatResponse}){
 return <div className="message-group">
  {message&&<div className="user-bubble">{message}</div>}
  {result&&<div className="assistant-card"><div className="assistant-label">KRISHINITI AI · GROUNDED RESPONSE</div><div className="answer">{result.answer}</div>
   {result.sources.length>0&&<div className="sources"><span>Retrieved knowledge</span>{result.sources.slice(0,3).map(s=><span className="source-chip" key={`${s.document}-${s.topic}`}>{s.topic} · {Math.round(s.score*100)}%</span>)}</div>}
  </div>}
 </div>;
}
