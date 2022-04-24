//javascript: /* omit the leading slashes when using as a bookmarklet; bookmarklet is to be used on the leetcode problem page */
(function(){
	function getDataUrl (url) { /* getting image as base64; a bit of overkill for the current task */
		return new Promise(function (resolve, reject) {
			var xhr = new XMLHttpRequest();
			xhr.open('GET',url);
			xhr.responseType = 'blob';
			xhr.send();
			
			xhr.onload = function () {
				if (xhr.status >= 200 && xhr.status < 300) {
					var reader = new FileReader();
					reader.onloadend = function() {
						resolve(reader.result);
					};
					reader.readAsDataURL(xhr.response);
				} else {
					reject({
						status: xhr.status,
						statusText: xhr.statusText
					});
				}
			};
			xhr.onerror = function () {
				reject({
					status: xhr.status,
					statusText: xhr.statusText
				});
			};
		});
	}
	
	let question_div = document.querySelector('[class*="question-content"]');
	if (question_div.length < 1) {
		alert ('Could not find description div');
		return;
	}
	let image_nodes = question_div.querySelectorAll('img');
	let promises = [];

	for (let i=0;i<image_nodes.length;i++) {
		promises.push(
			getDataUrl(image_nodes[i].src).then( /* TODO(?): process rejects properly */
				data_string => image_nodes[i].src = data_string
			)
		);
	};
	Promise.allSettled(promises).then( 
		v=>{
			let res = {};
			let title_div = document.querySelector('[data-cy*="question-title"]');
			let diff_div = document.querySelector('[data-cy*="description"] div[diff]');
			let diff = diff_div.textContent;
			let title = title_div.textContent;
			
			res['id'] = title.split('.')[0];
			res['title'] = title;
			res['difficulty'] = diff;
			res['description'] = question_div.innerHTML;
			
			navigator.clipboard.writeText(JSON.stringify(res));
			alert('Problem data saved to clipboard');
		}
	);
})()