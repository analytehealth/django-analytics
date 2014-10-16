var _es = escape;
var _ue = unescape;

// set cookie
function _sc(n, v, e, d) {
  document.cookie = n + "=" + _es(v) +
                    "; expires=" + e.toGMTString() +
                    "; path=/" + "; domain=" + d;
}

// get cookie
function _gc(n){
  var a = n + "=";
  var al = a.length;
  var cl = document.cookie.length;
  var i = 0;
  while(i < cl) {
    var j = i + al;
    if (document.cookie.substring(i, j) == a) return _gcv(j);
    i = document.cookie.indexOf(" ", i) + 1;
    if (i == 0) break;
  }
  return null;
}

// get cookie value
function _gcv(o){
  var e=document.cookie.indexOf (";", o);
  if (e == -1) e = document.cookie.length;
  return _ue(document.cookie.substring(o, e));
}

// get uuid cookie
var du = _gc("dja_uuid") || "{{ uuid }}";
var ued = new Date();
ued.setFullYear(ued.getFullYear() + 1);
_sc("dja_uuid", du, ued, "{{ domain }}");

//get tracking id cookie
var dti=_gc("dti") || "{{ tracking_id }}";
var sed = new Date();
sed.setTime(sed.getTime() + 30*60000);
_sc("dti", dti, sed, "{{ domain }}");

var img = document.createElement('img');
img.src = 'https://{{ capture_img_url }}' +
             '?dja_id={{ dja_id }}' +
             '&pth=' + window.location.pathname +
             '&qs=' +
             _es(window.location.search.substr(window.location.search.indexOf('?')+1)) +
             '&rf='+_es(document.referrer) +
             '&dti='+_es(dti)+'&du='+_es(du);
img.style.position = 'absolute';
img.style.left = '-999px';

document.getElementById('dja_tag').appendChild(img);
