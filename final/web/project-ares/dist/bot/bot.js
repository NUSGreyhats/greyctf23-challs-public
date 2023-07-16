const puppeteer = require('puppeteer')
const net = require('net')

const BASE_URL = process.env.BASE_URL || 'http://codestinks:3000'
const FLAG = process.env.FLAG || 'flag{test_flag}'

const browserPool = []

const getBrowser = async () => {
    if (browserPool.length > 0) {
        return browserPool.pop()
    }
    return await puppeteer.launch({
        headless: true,
        args: ['--js-flags=--jitless', '--no-sandbox', '--disable-setuid-sandbox']
    })
}

const returnBrowser = (browser) => {
    browserPool.push(browser)
}

const visitProfile = async (id) => {
    if (!id.match(/^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$/)) {
        return
    }
    const browser = await getBrowser()
    const page = await browser.newPage()
    const hostname = new URL(BASE_URL).hostname
    await page.setCookie({
        name: 'flag',
        value: FLAG,
        domain: hostname,
        path: '/',
        httpOnly: false,
        secure: false
    })
    try {
        await page.goto(BASE_URL + '/profile/' + id, { waitUntil: 'networkidle2', timeout: 5000 })
    }
    catch (e) {
        console.log(e)
    }
    await page.close()
    returnBrowser(browser)
}

setInterval(() => {
    while (browserPool.length > 0) {
        const browser = browserPool.pop()
        browser.close()
    }
}, 5 * 60 * 1000)

const server = net.createServer((socket) => {
    socket.on('data', async (data) => {
        const id = data.toString()
        await visitProfile(id)
    })
})

server.listen(3001, () => {
    console.log('Listening on port 3001')
})
