/**
 * Calcula el nivel de profundidad de un objeto.
 *
 * @param {Object} obj objeto con varios niveles de profundidad.
 * @return {Number} nivel de profundidad del objeto dado.
 */
const getLevel = (obj) => {
  let level = -2;
  if (obj && typeof obj === "object" && !Array.isArray(obj)) {
    for (let key in obj) {
      if (key === "enumfield" || key === "bitfield" ) {
        continue;
      }
      let depthOfKey = getLevel(obj[key]);
      if (depthOfKey > level) {
        level = depthOfKey;
      }
    }
    level++;
  }
  return level;
}

export {getLevel}