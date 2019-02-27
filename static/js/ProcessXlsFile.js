
function xw_xfer(data, cb,param) {
	var worker = new Worker('/static/js/xlsxworker2.js');
	worker.onmessage = function(e) {
		switch(e.data.t) {
			case 'ready': break;
			case 'e': console.error(e.data.d); break;
			default: xx=ab2str(e.data).replace(/\n/g,"\\n").replace(/\r/g,"\\r"); cb(JSON.parse(xx),param); break;
		}
	};
		var val = s2ab(data);
		worker.postMessage(val[1], [val[1]]);

}
function xw(data, cb,param) {
	 xw_xfer(data, cb,param);
}
function to_json(workbook) {
	var result = {};
    var t = {header: 1};
    for (var key in workbook.SheetNames) {
        var roa = XLS.utils.sheet_to_row_object_array(
            workbook.Sheets[workbook.SheetNames[key]], t);
        if (roa.length > 0) {
            result[0] = roa;
        }
        continue;
    }
	return result;
}


function ab2str(data) {
	var o = "", l = 0, w = 10240;
	for(; l<data.byteLength/w; ++l) o+=String.fromCharCode.apply(null,new Uint16Array(data.slice(l*w,l*w+w)));
	o+=String.fromCharCode.apply(null, new Uint16Array(data.slice(l*w)));
	return o;
}

function s2ab(s) {
	var b = new ArrayBuffer(s.length*2), v = new Uint16Array(b);
	for (var i=0; i != s.length; ++i) v[i] = s.charCodeAt(i);
	return [v, b];
}
