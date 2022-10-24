$(document).ready(function(){
  init_document_ready();
});

// - - - - - - - - - - - - - - - - - - - - - - - - - 
/* - - - - - - - - - - - - - - - - - - - - - - - - -
 * Anything that should be run as soon as DOM is 
 * loaded.
 * - - - - - - - - - - - - - - - - - - - - - - - - -
 */
 
function init_document_ready() {
  checkCookie();
}

// produce the unique id for every user
function setUniqueUserId() {
  var milliseconds = new Date().getTime();
  document.cookie = "unique_user_id" + "=" + milliseconds;
}

function getUniqueUserId() {
  let name = "unique_user_id=";
  let id = decodeURIComponent(document.cookie);
  if(id.indexOf(name) == 0) return id.substring(name.length, id.length);
  else return "";
}

function checkCookie() {
  let id = getUniqueUserId();
  if (id === "")  setUniqueUserId();
}