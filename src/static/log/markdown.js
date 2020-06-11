new SimpleMDE({
  autofocus: true,
  element: document.getElementById("logcontent"),
  spellChecker: false,
  lineWrapping: true,
  placeholder: "Type here...",
  hideIcons: ["side-by-side", "fullscreen"],
  shortcuts: {
    drawTable: "Cmd-Alt-T",
  },
  autoDownloadFontAwesome: true,
});
