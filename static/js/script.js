window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

const deleteVenueBtns = document.querySelectorAll(".delete-venue");
Array.from(deleteVenueBtns).forEach(item => {
  item.onclick = function (e){
    const id = e.target.dataset["id"];
    fetch("/venues/"+ id, {
      method: "DELETE",
    }).then(function(response) {
      window.location.href = "/"
    }).catch(function (){
      console.log("Error catch")
    })
  }
});