export type Source={document:string;topic:string;score:number};
export type ChatResponse={answer:string;assessment:string;recommended_actions:string[];what_to_monitor:string[];limitations:string[];sources:Source[];live_data_available:boolean;model:string;retrieval_used:boolean};
