const { fetchTopicsByDate, saveJson } = require('./tools')

async function fetchDate(year, month, date, saveList) {
    await fetchTopicsByDate(year, month, date)
        .then(res => res.json())
        .then(res => {
            console.log(`${year}/${month}/${date}`, res.length)
            const dateObj = new Date(year, month - 1, date)
            // saveJson(res, dateObj)
            saveList.push({
                time: dateObj.toLocaleDateString(),
                topics: res
            })
        })
}

async function main() {
    const loopDate = new Date('2017/05/09')
    const endDate = new Date()
    const saveList = []

    while (loopDate <= endDate) {
        const year = loopDate.getFullYear()
        const month = loopDate.getMonth() + 1
        const date = loopDate.getDate()
        await fetchDate(year, month, date, saveList)
        loopDate.setDate(loopDate.getDate() + 1)
    }

    saveJson(saveList, 'history_topics')
}

main()