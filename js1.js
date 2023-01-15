var flag = true; 
// 開關按鈕 -global var 只在onload後 加載一次, 之後每次更改只執行函數內而已
function show_menu(){
	var menu1 = document.getElementById('menu1');
	if(flag){
		menu1.style.display = 'block';
		flag = false;
	}else{
		menu1.style.display = 'none';
		flag = true;
	}
}

// 如果工作上同個專案內有多人經手維護的情況下，
// 用 onclick 的缺點就可能不小心覆蓋前人的 event handler，
// 而利用 addEventListener 就不會有這樣的問題囉
// https://ithelp.ithome.com.tw/articles/10191970

// 菜單隱藏
function show_menu1(){
	// alert('777');
	var menu1 = document.getElementById('menu1');
	menu1.style.display = 'none';
	flag = true;

}