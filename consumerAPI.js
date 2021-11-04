const consumer = kafka.consumer({ groupId: clientId })

const consume = async () => {

    await consumer.connect()
	await consumer.subscribe({ topic })
	await consumer.run({

        eachMessage: ({ message }) => {

            console.log(`data received: ${message.value}`)
		},
	})
}



consume().catch((err) => {
	console.error("error in consumer: ", err)
})