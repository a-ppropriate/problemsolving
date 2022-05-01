import 'https://cdn.jsdelivr.net/npm/vue/dist/vue.js';
import './components/problemsolving.js';

document.addEventListener('DOMContentLoaded',function(){
	let promises = [];
	let index = null;
	let constants = null;
	
	Promise.all(promises).then(values => {
		console.log(index);
		let app = new Vue ({
			el:'#app',
			template:'<problemsolving></problemsolving>',
			mounted:function(){
				console.log('app mounted');
			}
		});
	});
});