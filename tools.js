var fs = require('fs')
var fetch = require('node-fetch')

// https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do?date=2019/05/28&type=realTimeHotSearchList
async function fetchTopicByDate(year, month, date) {
    const res = fetch(`https://www.enlightent.cn/research/top/getWeiboHotSearchDayAggs.do?date=${year}/${month}/${date}&type=realTimeHotSearchList`)
    return res
}

var basePath = 'data/topics'
function saveJson(json, name) {
    const s = JSON.stringify(json, null, 2)
    const path = `${basePath}/${name}.json`

    fs.writeFileSync(path, s)
}

function test() {
    fetchTopicByDate(2019, 8, 28).then(
        res => console.log(res),
        err => console.log('Error: ', err)
    )
}

module.exports.fetchTopicsByDate = fetchTopicByDate
module.exports.saveJson = saveJson
module.exports.test = test
