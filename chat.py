import os, json, urllib.request, urllib.parse, ssl

def handler(request):
    try:
        body = request.json()
    except:
        body = {}
    user = (body.get("message") or "").strip()
    lower = user.lower()

    # If OPENAI_API_KEY env var is set, call OpenAI (completion)
    OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
    if OPENAI_KEY and user:
        try:
            prompt = (
                "Você é o Assistente Institucional da Fundação Interface Hub. "
                "Responda de forma formal, curta, objetiva e direcione para páginas do site quando aplicável.\n\n"
                f"Usuário: {user}\nAssistente:"
            )
            data = {
                "model":"text-davinci-003",
                "prompt": prompt,
                "max_tokens": 160,
                "temperature": 0.2
            }
            req = urllib.request.Request("https://api.openai.com/v1/completions",
                                         data=json.dumps(data).encode("utf-8"),
                                         headers={
                                             "Content-Type":"application/json",
                                             "Authorization": f"Bearer {OPENAI_KEY}"
                                         })
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                r = json.loads(resp.read().decode())
                text = r.get("choices",[{}])[0].get("text","").strip()
                if text:
                    return {"reply": text}
        except Exception:
            # fallback to rule-based below
            pass

    # Rule-based fallback (estilo GOV)
    if any(k in lower for k in ["oi","olá","ola","bom dia","boa tarde","olá"]):
        return {"reply":"Olá, sou o Assistente Virtual da Fundação Interface Hub. Em que posso ajudar hoje"}
    if "horário" in lower or "horario" in lower:
        return {"reply":"O horário de atendimento é de segunda a sexta, das 8h às 17h"}
    if "contato" in lower:
        return {"reply":"Os canais oficiais de contato estão na página Contato: contato@interfacehub.org"}
    if any(k in lower for k in ["documento","estatuto","relatório","relatorio","docs"]):
        return {"reply":"Os documentos públicos e relatórios estão disponíveis na página Transparência"}
    if "orçamento" in lower or "orcamento" in lower:
        return {"reply":"Para solicitar orçamento, acesse a página de Orçamentos e preencha o formulário"}
    # generic fallback
    return {"reply":"Solicitação recebida. Consulte as páginas oficiais ou peça um orçamento pela página de Orçamentos"}