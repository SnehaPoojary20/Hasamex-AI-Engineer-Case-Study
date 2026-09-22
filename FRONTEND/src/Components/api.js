const Base = "http://127.0.0.1:8000";


async function req(path, opts){
     const res = await fetch(Base+path,opts);

     if(! res.ok){
        throw new Error(await(res.text));
     }

     return res.json;
}


export const getGuide = ()=>req("/api/guide");

export const getThemes =()=> req("/api/themes");

export const askQuestions =(question)=>
    req(
        "/api/ask",{
           method: "POST",
           headers: { "Content-Type": "application/json" },
           body: JSON.stringify({ question }),
        }
    );