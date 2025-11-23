function pesquisar(){
  const q = (document.getElementById('campoBusca')||{value:''}).value.toLowerCase().trim();
  if(!q){ alert('Digite o termo de busca'); return; }
  if(q.includes('transpar')) return location.href='transparencia.html';
  if(q.includes('orc') || q.includes('orçam')) return location.href='orcamentos.html';
  if(q.includes('port') || q.includes('proj')) return location.href='portfolio.html';
  if(q.includes('chat') || q.includes('atend')) return location.href='chatbot.html';
  alert('Nenhum resultado encontrado no site');
}