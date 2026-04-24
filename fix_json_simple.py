import json

# 手动构建正确的JSON对象
book_source = {
    "bookSourceComment": "二次优化版：补充ruleExplore发现页解析规则，ruleBookInfo补充kind/lastChapter字段，修正首页分页参数，优化搜索author格式。首次优化：清理URL末尾##，header改为浏览器UA，respondTime优化至30s，searchUrl添加key编码，添加bookUrlPattern。 | 修复：header恢复为okhttp/4.12.0（API接口型网站需要） | 修复：canHeadUrl增加GET fallback和timeout至5秒 | 修复：更新域名和URL模式以适配新网站结构",
    "bookSourceGroup": "听书",
    "bookSourceName": "🗨️ 悦听吧",
    "bookSourceType": 1,
    "bookSourceUrl": "http://yuetingba.cn",
    "bookUrlPattern": "https?://www.yuetingba.cn/book/detail/[a-f0-9-]+/[0-9]+",
    "customButton": False,
    "customOrder": 4,
    "enabled": True,
    "enabledCookieJar": True,
    "enabledExplore": True,
    "eventListener": False,
    "exploreUrl": "@js:var tagStyle={layout_flexGrow:1,layout_flexShrink:1,layout_alignSelf:'auto',layout_flexBasisPercent:0.29,layout_wrapBefore:false};var tabs=[['首页','/'],['最新','/top/latest/{{page}}'],['推荐','/top/recommend/{{page}}'],['玄幻','/book/1/{{page}}'],['历史','/book/2/{{page}}'],['武侠','/book/3/{{page}}'],['都市','/book/4/{{page}}'],['科幻','/book/5/{{page}}'],['名著','/book/6/{{page}}'],['女频','/book/7/{{page}}'],['社科','/book/8/{{page}}'],['儿童','/book/9/{{page}}']];JSON.stringify(tabs.map(function(it){return {title:it[0],url:it[1],style:tagStyle};}))",
    "header": '{"User-Agent":"okhttp/4.12.0","Accept-Encoding":"identity"}',
    "jsLib": '''var __legadoJava = null;

function bindEnv(java) {
    __legadoJava = java;
}

function getLegadoJava() {
    if (__legadoJava) return __legadoJava;
    try {
        if (java) return java;
    } catch (e) {}
    throw 'Legado java helper unavailable';
}

function getAudioHeaders() {
    return {
        'User-Agent': 'okhttp/4.12.0',
        'Accept-Encoding': 'identity'
    }
}

function getAudioHeadersJson() {
    return JSON.stringify(getAudioHeaders());
}

function AesDecode(data) {
    var java = getLegadoJava();
    var key = java.base64DecodeToByteArray('le95G3hnFDJsBE+1/v9eYw==');
    var iv = java.base64DecodeToByteArray('IvswQFEUdKYf+d1wKpYLTg==');
    return java.createSymmetricCrypto('AES/CBC/PKCS7Padding', key, iv).decryptStr((data + '').replace(/\\n/g, ''));
}

function gk(t, n) {
    var result = '';
    var i;
    for (i = 0; i < 20; i++) {
        result += String.fromCharCode(t.charCodeAt(i) + Number(n.charAt(i)));
    }
    for (i = 20; i < t.length; i++) {
        result += String.fromCharCode(t.charCodeAt(i) + Number(n.charAt(i - 20)));
    }
    return result;
}

function gi(t, n) {
    var result = '';
    var i;
    for (i = 20; i > 4; i--) {
        result += String.fromCharCode(t.charCodeAt(i) + Number(n.charAt(i - 1)));
    }
    return result;
}

function d(e, t, n) {
    var java = getLegadoJava();
    var key = gk(t, n);
    var iv = gi(t, n);
    e = (e + '').replace(/\\n/g, '');
    return java.createSymmetricCrypto('AES/CBC/PKCS7Padding', key, iv).decryptStr(e);
}

function fixAsslInfo(assl, es) {
    var result = {
        assl: assl,
        sk: 'xMiP5W1DHBxC5PwQ5oj5QfRn0tsT5UBk'
    }
    es = Number(es || 0);
    if (es < 300) {
        es = parseInt(assl.substring(0, 1).charCodeAt(0), 10);
        if (assl.length - 32 > es) {
            result.sk = assl.substring(es, es + 32);
            result.assl = assl.substring(0, es) + assl.substr(es + 32);
        } else {
            result.sk = assl.substr(assl.length - 32);
            result.assl = assl.substr(0, assl.length - 32);
        }
    } else {
        result.assl = assl.replace(result.sk, '');
    }
    return result;
}

function buildServerUrl(item) {
    if (!item) return '';
    if (String(item.Type) == 'AAAA') {
        return item.Scheme + '://[' + item.Value + ']:' + item.Port;
    }
    return item.Scheme + '://' + item.Value + ':' + item.Port;
}

function getBookSuffix(bookId) {
    var ids = String(bookId || '').split('-');
    if (ids.length > 4) return ids[4];
    return '';
}

function scoreAudioServer(item, suffix) {
    var score = 0;
    var bookIds = item && item.BookIds ? String(item.BookIds) : '';
    if (suffix && bookIds.indexOf(suffix) >= 0) {
        score += 1000;
    } else if (!bookIds) {
        score += 100;
    }
    if (String(item.Type) == 'A') {
        score += 10;
    }
    score += Number(item.Ratio || 0);
    return score;
}

function orderAudioServers(list, bookId, supportIpv6) {
    var audioList = list.filter(function(item) {
        return String(item.AsType) == '1';
    });
    if (audioList.length == 0) {
        audioList = list.filter(function(item) {
            return String(item.AsType) == '2';
        });
    }
    if (!supportIpv6) {
        audioList = audioList.filter(function(item) {
            return String(item.Type) == 'A';
        });
    }
    var suffix = getBookSuffix(bookId);
    audioList.sort(function(a, b) {
        return scoreAudioServer(b, suffix) - scoreAudioServer(a, suffix);
    });
    return audioList;
}

function pickPreferredServer(list, bookId, supportIpv6) {
    var ordered = orderAudioServers(list, bookId, supportIpv6);
    if (ordered.length == 0) return '';
    return buildServerUrl(ordered[0]);
}

function extractFileName(url) {
    var m = String(url || '').match(/\/([^\/?#]+)(\?[^#]*)?$/);
    return m ? m[1] : '';
}

function buildRawPlayUrl(audioServer, path) {
    return encodeURI(String(audioServer || '') + String(path || ''));
}

function buildTokenPlayUrl(audioServer, path, sk) {
    var java = getLegadoJava();
    var raw = buildRawPlayUrl(audioServer, path);
    if (!sk) return raw;
    var fileName = extractFileName(raw);
    if (!fileName) return raw;
    var expire = Math.floor(new Date().getTime() / 1000) + 600;
    var token = java.md5Encode(fileName + '|' + expire + '|' + sk);
    return raw + '?token=' + token + '&expire=' + expire;
}

function buildPlayUrlByMode(audioServer, path, sk, mode) {
    if (mode == 'token') {
        return buildTokenPlayUrl(audioServer, path, sk);
    }
    return buildRawPlayUrl(audioServer, path);
}

function buildCandidateItems(serverList, bookId, supportIpv6, path, sk) {
    var ordered = orderAudioServers(serverList, bookId, supportIpv6);
    var result = [];
    ordered.forEach(function(item) {
        var base = buildServerUrl(item);
        result.push({
            base: base,
            mode: 'raw',
            url: buildRawPlayUrl(base, path)
        });
        result.push({
            base: base,
            mode: 'token',
            url: buildTokenPlayUrl(base, path, sk)
        });
    });
    return result;
}

function canHeadUrl(url, headersJson, timeout) {
    var java = getLegadoJava();
    try {
        java.head(url, headersJson, timeout || 5000);
        return true;
    } catch (e) {
        try {
            var opts = JSON.parse(headersJson || '{}');
            opts.method = 'GET';
            opts.timeout = timeout || 5000;
            java.get(url, opts);
            return true;
        } catch (e2) {
            return false;
        }
    }
}

function pickPlayableItem(items, headersJson) {
    var i;
    if (!items || items.length == 0) return null;
    for (i = 0; i < items.length; i++) {
        if (canHeadUrl(items[i].url, headersJson, 2500)) {
            return items[i];
        }
    }
    return items[0];
}

function wrapPlayUrl(url, headersJson) {
    if (!url) return '';
    return url + ',{"headers":' + headersJson + '}';
}''',
    "lastUpdateTime": 1777044525112,
    "respondTime": 180000,
    "ruleBookInfo": {
        "author": ".books-detail-info@.info-rows@.row-item.0@span.1@text",
        "coverUrl": ".books-detail-cover@img@src",
        "intro": ".books-detail@.container.0@.row@div[-4:-1]@html",
        "kind": ".books-detail-info@.info-rows@.row-item@text",
        "lastChapter": ".books-detail-info@.info-rows@.row-item:last-child@text",
        "name": "h1.book-detail-title@text"
    },
    "ruleContent": {
        "content": "@js:bindEnv(java);try {var $ = JSON.parse(src);var n = $.id.replace(/[-]/g, '');var i = $.creationTime.replace(/[-:T. ]/g, '');while (i.length < 20) {i += '0';}var path = d($.efi, n, i);var audioSk = java.get('audioSk');var audioBookId = java.get('audioBookId') || $.bookId || '';var supportIpv6 = java.get('audioSupportIpv6') == '1';var serverListText = java.get('audioServerList');var serverList = [];if (serverListText) {try {serverList = JSON.parse(serverListText);} catch (e) {}}if (serverList.length == 0) {var preferred = java.get('audioServer');if (preferred) {try {serverList = [{Scheme: preferred.split('://')[0],Value: preferred.replace(/^https?:\/\//, '').replace(/:\d+$/, ''),Port: preferred.match(/:(\d+)$/) ? preferred.match(/:(\d+)$/)[1] : '',Type: 'A',AsType: '1',Ratio: 0,BookIds: null,CateNos: null}];} catch (e) {}}if (serverList.length == 0) {result = '';} else {var headersJson = java.get('audioHeaders') || getAudioHeadersJson();var items = buildCandidateItems(serverList, audioBookId, supportIpv6, path, audioSk);if (items.length == 0) {result = '';} else {var playableItem = pickPlayableItem(items, headersJson);result = wrapPlayUrl(playableItem ? playableItem.url : '', headersJson);}}}} catch (e) {result = '';}"
    },
    "ruleExplore": {
        "author": "span@title##\n## 演播：",
        "bookList": ".section-box-list-item",
        "bookUrl": "a.0@href",
        "coverUrl": "img@src",
        "intro": ".box-list-item-text-intro@text",
        "kind": ".section-box-list-item@.tag-info@text",
        "name": ".box-list-item-text-title@text"
    },
    "ruleSearch": {
        "author": "span@title##\\n##演播：",
        "bookList": ".section-box-list-item",
        "bookUrl": "a.0@href",
        "coverUrl": "img@src",
        "intro": ".box-list-item-text-intro@text",
        "name": ".box-list-item-text-title@text"
    },
    "ruleToc": {
        "chapterList": "@js:bindEnv(java);try {var l = java.getElements('.ting-list-content-item>.col-md-10>a');var asslMatch = src.match(/var\s+assl\s*=\s*'([^']+)/);var esMatch = src.match(/var\s+es\s*=\s*'([^']+)/);var bookIdMatch = src.match(/var\s+bookId\s*=\s*'([^']+)/);if (!asslMatch || !bookIdMatch) {list = [];} else {var assl = asslMatch[1];var bookId = bookIdMatch[1];var supportIpv6 = false;var fixed = fixAsslInfo(assl, esMatch ? esMatch[1] : 0);var decrypted = AesDecode(fixed.assl);var serverList = JSON.parse(decrypted);var preferred = pickPreferredServer(serverList, bookId, supportIpv6);java.put('audioServerList', JSON.stringify(serverList));java.put('audioBookId', bookId);java.put('audioSupportIpv6', supportIpv6 ? '1' : '0');java.put('audioServer', preferred);java.put('audioSk', fixed.sk);java.put('audioHeaders', getAudioHeadersJson());list = [];l.forEach(function(a) {var text = a.text();var onclick = a.attr('onclick') || '';var idMatch = onclick.match(/'([^']+)/);if (idMatch) {var id = idMatch[1];list.push({text: text, href: '/api/app/docs-listen/' + id + '/ting-with-efi'});}});}} catch (e) {list = [];}",
        "chapterName": "text",
        "chapterUrl": "href",
        "nextTocUrl": "ul[role=\"tablist\"]@li@a@href"
    },
    "searchUrl": "@js:'http://yuetingba.cn/Search?type=1&name='+java.encodeURI(key)",
    "weight": 0
}

# 保存为JSON文件
with open('/workspace/悦听吧_fixed.json', 'w', encoding='utf-8') as f:
    json.dump([book_source], f, ensure_ascii=False, indent=2)

print('修复后的JSON已保存到 /workspace/悦听吧_fixed.json')
