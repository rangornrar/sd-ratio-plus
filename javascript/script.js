onUiLoaded(() => {
  const ratioMap = {
    "4:3": 4 / 3,
    "3:2": 3 / 2,
    "16:9": 16 / 9,
    "1:1": 1,
    "2:3": 2 / 3,
    "3:4": 3 / 4
  };

  const getElem = id => gradioApp().querySelector(`#${id}`);

  const ratioSelect = getElem("aspect_ratio_select");
  const widthInput = getElem("width_input");
  const heightInput = getElem("height_input");
  const lockCheckbox = getElem("lock_aspect_ratio");
  const useHeightAsBase = getElem("use_height_as_base");
  const roundTo64 = getElem("round_to_64");

  const roundMultiple = (val, mult) => Math.round(val / mult) * mult;

  const updateDimensions = () => {
    if (!lockCheckbox?.checked) return;

    const ratioKey = ratioSelect?.value;
    const ratio = ratioMap[ratioKey];
    const useHeight = useHeightAsBase?.checked;
    const round = roundTo64?.checked;

    if (!ratio || !widthInput || !heightInput) return;

    if (useHeight) {
      const height = parseInt(heightInput.value);
      if (!isNaN(height)) {
        let newWidth = height * ratio;
        if (round) newWidth = roundMultiple(newWidth, 64);
        widthInput.value = Math.round(newWidth);
      }
    } else {
      const width = parseInt(widthInput.value);
      if (!isNaN(width)) {
        let newHeight = width / ratio;
        if (round) newHeight = roundMultiple(newHeight, 64);
        heightInput.value = Math.round(newHeight);
      }
    }
  };

  [ratioSelect, widthInput, heightInput, lockCheckbox, useHeightAsBase, roundTo64].forEach(el => {
    if (el) el.addEventListener("change", updateDimensions);
    if (el) el.addEventListener("input", updateDimensions);
  });
});
