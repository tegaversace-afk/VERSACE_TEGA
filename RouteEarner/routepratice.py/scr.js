const driverProfile  = {
    name :"Aboki",
    deliveries : 35,
    payment : {
        wallet : 15000,
        bonus : 5000,
        fuel : 1000

    }


}
console.log(driverProfile.wallet);
console.log(driverProfile.payment.bonus);

const {
    payment: {wallet,bonus,fuel}
} = driverProfile ;
console.log(wallet);
console.log(fuel);

const driver = {
    name : 'Tega',
    deliveries : 30,
    wallet : 5000

};
const updatedDriver = {
    ...driver,
    wallet : 7500
};

console.log(updatedDriver)

const driverr = {
    name : "Tega",
    deliveries : 25,
    wallet : 42500
};
const promotedDriver = {
    ...driverr, 
    deliveries : 40,
    wallet : 60000,
    status : "experienced"
};

console.log(promotedDriver);

const driverNames = ["Tega", "John", "Mary", "David", "Peter"];
const [ firstDriver, ...otherDriver] = driverNames;
console.log(firstDriver);
console.log(otherDriver)

const driverrr = {
    name : "Tega",
    deliveries : 25,
    wallet : 42500
};
const upddriv ={
    rating : 4.5,
    location : 'CHOBA',
    ...driverrr

};
console.log(upddriv.rating)

const driverInfo = {
    name: "Tega",
    deliveries: 30,
    wallet: 45000,
    status: "Experienced"
};
const { name, ...drInfo} = driverInfo;
console.log(name);
console.log(drInfo);

const routeDrivers = ["Tega", "John", "Mary", "David", "Peter"];
const [firdriver, secdriver,...otherDrive] = routeDrivers;
console.log(firdriver);
console.log(secdriver);
console.log(otherDrive);

const driverInfoo = {
    name: "Tega",
    deliveries: 30,
    wallet: 45000,
    status: "Experienced",
    location: "Port Harcourt"
};
const {
    name :driverName,  wallet :driverWallet,...otherDetails

} = driverInfo;
console.log(driverName);
console.log(driverWallet);
console.log(otherDetails);


console.log(data.drivers[2].name)
console.log(data.drivers[0].wallet)
console.log(data.drivers)
