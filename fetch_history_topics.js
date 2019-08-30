const { fetchTopicsByDate, saveJson } = require('./tools')

function fetchDate(year, month, date, saveList) {
  return fetchTopicsByDate(year, month, date)
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
    .catch(res => res)
}

async function main() {
  const loopDate = new Date('2017/05/09')
  const endDate = new Date()
  const saveList = []

  const promiseList = []

  while (loopDate <= endDate) {
    const year = loopDate.getFullYear()
    const month = loopDate.getMonth() + 1
    const date = loopDate.getDate()
    // await fetchDate(year, month, date, saveList)
    promiseList.push(fetchDate(year, month, date, saveList))
    loopDate.setDate(loopDate.getDate() + 1)
  }

  console.log(promiseList[0])

  Promise.all(promiseList).then(
    () => {
      console.log('Fetched ', saveList.length, 'records')
      saveJson(saveList, 'history_topics_async')
    }
  ).catch(
    (err) =>  {
      console.log('Fetched ', saveList.length, 'records')
      console.log('Error occurs: ')
      console.log(err)
      saveJson(saveList, 'history_topics_async')
    }
  )

  
}

main()