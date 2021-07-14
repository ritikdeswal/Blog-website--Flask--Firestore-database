

function changeit(id) {
var flag=id.getAttribute("name");
if (flag=="dark") {
  id.setAttribute("name","light");
  document.documentElement.style.setProperty('--bgclr', 'white');
  document.documentElement.style.setProperty('--txtclr', 'black');
  document.documentElement.style.setProperty('--footerclr', '#d9d9d9');

}
if (flag=="light") {
  id.setAttribute("name","dark");
  document.documentElement.style.setProperty('--bgclr', '#1a1b1c');
  document.documentElement.style.setProperty('--txtclr', 'white');
  document.documentElement.style.setProperty('--footerclr', '#262729');
}
}


//  function change(p) {
//    document.documentElement.style.setProperty('--txt-clr', '#008800');
//  }

