function blink(){
    let x = document.querySelector('.blink');
    if (x.style.visibility === 'hidden')
    {
        x.style.visibility = 'visible';
    }
    else
    {
        x.style.visibility = 'hidden';
    }
}

    window.setInterval(blink, 500);

function show(id) {
    document.getElementById(id).style.visibility = "visible";
  }
function hide(id) {
    document.getElementById(id).style.visibility = "hidden";
  }
function pollresults(){

    //todo still oesnt work
    document.getElementById(poll).innerHTML = "100% of voters liked the creator of this page!"
}