document.addEventListener('DOMContentLoaded',function(){
	let app = new Vue ({
		el:'#app',
		data: function() {
			return {
				text: 'stub'
			}
		},
		mounted:function(){
			console.log('app mounted');
		}
	});
});