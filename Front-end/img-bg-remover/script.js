let dropZone = document.getElementById("dropZone");
let fileInput = document.getElementById("fileInput");

fileInput.addEventListener("change", function () {
  if (fileInput.files.length > 0) {
    uploadFile(fileInput.files[0]);
  }
});

dropZone.addEventListener("dragover", function (e) {
  e.preventDefault();
  this.classList.add("dragover");
});

dropZone.addEventListener("dragleave", function (e) {
  e.preventDefault();
  this.classList.remove("dragover");
});

dropZone.addEventListener("drop", function (e) {
  e.preventDefault();
  this.classList.remove("dragover");

  let file = e.dataTransfer.files[0];
  if (file) {
    uploadFile(file);
  }
});

async function uploadFile(file) {
  let formData = new FormData();
  formData.append("file", file);

  try {
    let response = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Failed to upload file");
    }

    let blob = await response.blob();
    let url = window.URL.createObjectURL(blob);

    let a = document.createElement("a");
    a.href = url;
    a.download = file.name.replace(".png", "") + "_rmbg.png";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Error:", error);
  }
}