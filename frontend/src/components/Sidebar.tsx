import {Sprout,ShieldCheck,Database,Languages,BrainCircuit} from "lucide-react";
export function Sidebar(){
 return <aside className="sidebar">
  <div className="brand"><div className="brand-icon"><Sprout size={23}/></div><div><strong>KrishiNiti AI</strong><span>Smart Farming Advisor</span></div></div>
  <div className="side-section"><div className="side-title">Knowledge domains</div>
   {["Crop & Season","Soil & Nutrients","Irrigation","Pest & Disease","Weather-Aware","Market & Mandi"].map(x=><div className="side-item" key={x}>{x}</div>)}
  </div>
  <div className="side-card"><ShieldCheck size={18}/><div><strong>Grounded advice</strong><p>Responses are grounded in the agricultural knowledge base.</p></div></div>
  <div className="side-card"><Database size={18}/><div><strong>RAG powered</strong><p>Semantic retrieval with ChromaDB and IBM embeddings.</p></div></div>
  <div className="side-card"><BrainCircuit size={18}/><div><strong>IBM Granite</strong><p>Context-aware response generation via watsonx.ai.</p></div></div>
  <div className="side-footer"><span><Languages size={15}/> English · ಕನ್ನಡ · हिन्दी</span></div>
 </aside>;
}
