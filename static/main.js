function Show(url, type, fileType = "") {
  console.log(type, url);
  document.getElementById("file").style.display = "flex";
  if (type == "img") {
    document.getElementById("img").style.display = "block";
    document.getElementById("img").src = url;
  } else if (type == "audio") {
    document.getElementById("audio").style.display = "block";
    document.getElementById(
      "sourceA"
    ).src = `${location.protocol}//${location.host}${url}`;
    document.getElementById("sourceA").type = fileType;
  } else if (type == "video") {
    document.getElementById("video").style.display = "block";
    document.getElementById("sourceV").src = url;
    document.getElementById("sourceV").type = fileType;
  }
}
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    document.getElementById("img").style.display = "none";
    document.getElementById("audio").style.display = "none";
    document.getElementById("file").style.display = "none";
    document.getElementById("video").style.display = "none";
    document.getElementById("sourceA").src = "";
    document.getElementById("sourceV").src = "";
    document.getElementById("sourceV").type = "";
    document.getElementById("sourceA").type = "";
  }
});

function loadMp3(url, id) {
  jsmediatags.read(`${location.protocol}//${location.host}${url}`, {
    onSuccess: function (tag) {
      console.log(tag);
      const data = tag.tags.picture.data;
      let image = tag.tags.picture;
      if (image) {
        var base64String = "";
        for (var i = 0; i < image.data.length; i++) {
          base64String += String.fromCharCode(image.data[i]);
        }
        var base64 = "data:image/jpeg;base64," + window.btoa(base64String);
        console.log(base64);
        document.getElementById(id).setAttribute("src", base64);
      }
    },
    onError: function (error) {
      console.log(error);
    },
  });
}
