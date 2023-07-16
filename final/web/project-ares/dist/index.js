const express = require('express')
const pug = require('pug')
const uuid = require('uuid')

const app = express()

app.set('view engine', 'pug')

app.use(express.static('public'))
app.use(express.urlencoded({ extended: true }))

const profiles = new Map()

app.get('/', (req, res) => {
    res.render('index')
})

app.post('/signup', (req, res) => {
    const profile = req.body
    const id = uuid.v4()
    profile.id = id
    profiles.set(id, profile)
    res.redirect('/profile/' + id)
})

app.get('/profile/:id', (req, res) => {
    const id = req.params.id
    const profile = profiles.get(id)
    res.render('profile', profile)
})

app.get('/delete/:id', (req, res) => {
    const id = req.params.id
    profiles.delete(id)
    res.redirect('/')
})

app.get('/submit/:id', (req, res) => {
    const id = req.params.id
    if (!id.match(/^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$/)) {
        res.send('Invalid ID')
        return
    }
    const net = require('net')
    const client = new net.Socket()
    client.connect(3001, 'ares-bot', () => {
        client.write(id)
        client.destroy()
    })
    res.send('Submitted')
})

app.listen(3000, () => {
    console.log('Listening on port 3000')
})
