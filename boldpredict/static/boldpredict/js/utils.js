String.prototype.format = function () {
    let self = this;
    for (let k in arguments) {
        self = self.replace(new RegExp("\\{" + k + "\\}", 'g'), arguments[k]);
    }
    return self
};

randID = function(length) {
   let result           = '';
   let characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   let charactersLength = characters.length;
   for (let i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
};

replaceEventListener = function(selector, event, listener) {
    let older = $(selector)[0];
    let newer = older.cloneNode(true);
    newer.addEventListener(event, listener);
    older.parentNode.replaceChild(newer, older);
    return newer;
};