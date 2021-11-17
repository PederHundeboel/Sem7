
const { Kafka } = require("kafkajs")

const clientId = "app-api"

const brokers = ["localhost:9092"]

const topic = "found"



const kafka = new Kafka({ clientId, brokers })
const consumer = kafka.consumer({ groupId: clientId })

const consume = async () => {

    await consumer.connect()
	await consumer.subscribe({ topic })
	await consumer.run({

        eachMessage: ({ message }) => {

            console.log(`Data received: ${message.value}`)
		},
	})
}



module.exports = consume