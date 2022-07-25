document.addEventListener('DOMContentLoaded', ()=> {
  const timer = document.getElementById("timer");
  const mfa = document.getElementById("code-mfa");
  const new_code = document.getElementById("new-code-button");
  const verify = document.getElementById("verify-button");
  const title = document.getElementById("title");
  const info = document.getElementById("extra-info");


  function initiate_counter(time) {
    timer.textContent = time;
    title.textContent = "Code sending to Arduino in";
    timer.style.display = "";
    info.style.display = "";
    mfa.style.display = "none";
    verify.style.display = "none";
    new_code.style.display = "none";
    countdown(time);
  }

  function countdown(time) {
    timer.textContent = time;
    if (time == 0) {
      title.textContent = "Code sent";
      timer.style.display = "none";
      info.style.display = "none";
      mfa.style.display = "";
      new_code.style.display = "";
      verify.style.display = "";
      return;
    }
    window.setTimeout(() => {
      countdown(time - 1);
    }, 1000);

  }

  initiate_counter(3);
});
 