

class P {
    constructor() {
        this.jeje = "P's jej"
    }
    l() {
        console.log(this.jeje)
    }
}




class J {
    constructor() {
        this.jeje = "yeey my jej"
    }
    jej(l) {
        l()
    }
}


const j = new J()
const p = new P()


j.jej(p.l.bind(p))

p.l.bind(j)()
