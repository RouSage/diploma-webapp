loadImage = function() {
  document.getElementById('image').click();
};

document.getElementById('recognitionLink').onclick = function(e) {
  e.preventDefault();
  loadImage();
};

if (document.getElementById('loadImageBtn') != null) {
  document.getElementById('loadImageBtn').onclick = function() {
    loadImage();
  };
}

if (document.getElementById('uploadForm') != null) {
  document.getElementById('image').onchange = function() {
    document.getElementById('uploadForm').submit();
  };
}
