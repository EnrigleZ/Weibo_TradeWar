const { fetchTopicsByDate, saveJson } = require('./tools')

function fetchDate(year, month, date) {
    fetchTopicsByDate(year, month, date)
        .then(res => res.json())
        .then(res => {
            console.log(res.length)
            const dateObj = new Date(year, month - 1, date)
            saveJson(res, dateObj)
        })
}

function main() {
    const loopDate = new Date('2017/05/09')
    const endDate = new Date()
    while (loopDate <= endDate) {
        const year = loopDate.getFullYear()
        const month = loopDate.getMonth() + 1
        const date = loopDate.getDate()
        fetchDate(year, month, date)
        loopDate.setDate(loopDate.getDate() + 1)
    }
}

main()