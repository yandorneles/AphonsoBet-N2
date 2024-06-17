function mostraMsgValidacao(msg){
  alert(msg);
}


(() => {
  const formApostar = document.querySelector("#formApostar");
  if (formApostar) {
    formApostar.addEventListener("submit", (event) => {
      event.preventDefault();
      
      if(parseFloat(event.target.inputJogoId.value) == 0){
        mostraMsgValidacao("Informações do Jogo não encontradas!");
        return false;
      }
      else if(parseFloat(event.target.inputTimeCasaId.value) == 0){
        mostraMsgValidacao("Informações do time da casa não encontradas!");
        return false;
      }
      else if(parseFloat(event.target.inputTimeCasaPontos.value) < 0){
        mostraMsgValidacao("Os pontos não podem zero igual a zero!");
        return false;
      }
      else if(parseFloat(event.target.inputTimeForaId.value) == 0){
        mostraMsgValidacao("Informações do time de fora não encontradas!");
        return false;
      }
      else if(parseFloat(event.target.inputTimeForaPontos.value) < 0){
        mostraMsgValidacao("Os pontos não podem zero igual a zero!");
        return false;
      }
      else if(parseFloat(event.target.inputValor.value) == 0){
        mostraMsgValidacao("O valor da aposta deve ser maior que zero!");
        return false;
      }
      else{
        event.target.removeEventListener("submit", (e) => {});
        return formApostar.submit();
      }
    });
  }
})();
