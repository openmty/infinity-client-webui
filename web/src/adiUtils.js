function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function getRandomFloat(min, max) {
        return Math.random() * (max - min) + min;
    }

// 时间戳转时间
function timestampToTime(timestamp) {
    let date = new Date(timestamp * 1000); // 时间戳为10位需*1000，时间戳为13位的话不需乘1000
    let Y = date.getFullYear() + '-'   ;    
    let M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-';
    let D = (date.getDate() < 10 ? '0'+(date.getDate()) : date.getDate()) + ' ';
    let h = (date.getHours() < 10? '0'+(date.getHours()) : date.getHours()) + ':';
    let m = (date.getMinutes() < 10? '0'+(date.getMinutes()) : date.getMinutes()) + ':';
    let s = (date.getSeconds() < 10? '0'+(date.getSeconds()) : date.getSeconds());
    return Y+M+D+' '+h+m+s   
}
//string转base64
function stringToBase64(str) {
    return btoa(unescape(encodeURIComponent(str)));
}
//base64转string
function base64ToString(str) {
    return decodeURIComponent(escape(atob(str)));
}
// 获取当前时间戳
function getCurrentTime() {
    return Date.now();
}
// 获取当前时间
function getCurrentTimeString() {
    return this.timestampToTime(this.getCurrentTime());
}
// md5加密
function md5(str) {
    return CryptoJS.MD5(str).toString();
}
// 封装fetch为同步方法
async function adiFetch(url, method, body, headers) {
    let res = await fetch(url, {
        method: method,
        headers: headers?headers:{
            'Content-Type': 'application/json'
        },
        body: body
    });
    const _data = await res.json(); 
    return _data;
}
export default {
    getRandomInt,
    getRandomFloat,
    timestampToTime,
    stringToBase64,
    base64ToString,
    getCurrentTime,
    getCurrentTimeString,
    md5,
    adiFetch
};