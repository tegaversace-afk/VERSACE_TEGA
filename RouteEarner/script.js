const button = document.getElementById("show-message-btn");
const message = document.getElementById("message");

const completedDeliveries = 40;

if (button && message) {
    button.addEventListener("click", function () {
        if (message.hidden) {
            message.textContent = `You have completed ${completedDeliveries} deliveries!`;
            message.hidden = false;
            button.textContent = "Hide Message";
        } else {
            message.hidden = true;
            button.textContent = "Show Message";
        }
    });
}

const filterButtons = document.querySelectorAll("[data-filter]");

const deliveryRows = document.querySelectorAll(".delivery-row");

const deliveryCount = document.getElementById("delivery-count");

filterButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        const selectedStatus = button.dataset.filter;

        let visibleCount = 0;

        deliveryRows.forEach(function (row) {
            if (
                selectedStatus === "all" ||
                row.dataset.status === selectedStatus
            ) {
                row.hidden = false;
                visibleCount++;
            } else {
                row.hidden = true;
            }
        });

        deliveryCount.textContent =
    `Showing ${visibleCount} ${visibleCount === 1 ? "delivery" : "deliveries"}`;
    });
});

const activeDeliveries = 0;

const deliveryStatus =
    activeDeliveries > 0 ? "You have an active delivery." : "You have no active deliveries.";

console.log(deliveryStatus);



function calculateDriverWallet(deliveries, paymentPerDelivery) {
    const earnings = deliveries * paymentPerDelivery;

    let bonus = 0;

    if (deliveries >= 20) {
        bonus = 5000;
    }

    const total = earnings + bonus;

    return {
        earnings: earnings,
        bonus: bonus,
        total: total
    };
}

const driver = calculateDriverWallet(25, 1500);

console.log(driver);
console.log(driver.earnings);
console.log(driver.bonus);
console.log(driver.total);

const drivers = ["Tega", "John", "Mary", "David"];

console.log(drivers);

const routeDrivers = ["Tega", "John", "Mary"];

routeDrivers.push("David");

console.log(routeDrivers);
console.log(routeDrivers.length);

routeDrivers.push("David");

for (let i = 0; i < routeDrivers.length; i++) {
    console.log(routeDrivers[i]);
}
for (const driver of routeDrivers) {
    console.log("Registered driver:", driver);
}
const registeredDrivers = [
    {
        name: "Tega",
        deliveries: 25,
        wallet: 37500
    },
    {
        name: "John",
        deliveries: 15,
        wallet: 22500
    },
    {
        name: "Mary",
        deliveries: 30,
        wallet: 45000
    }
];
const experiencedDrivers = registeredDrivers.filter(
    driver => driver.deliveries >= 20
);

console.log(experiencedDrivers);
for (const driver of experiencedDrivers) {
    console.log(driver.name);
    console.log(driver.deliveries);
    console.log(driver.wallet);
}
const driverNames = registeredDrivers.map(driver => driver.name);

console.log(driverNames);
const qualifiedDriverNames = registeredDrivers
    .filter(driver => driver.deliveries >= 20
    )

    .map(driver => driver.name
    );
    

console.log(qualifiedDriverNames);
const selectedDriver = registeredDrivers.find(
    driver => driver.name === "John"
);

console.log(selectedDriver);

const hasExperiencedDriver = registeredDrivers.some(
    driver => driver.deliveries >= 35
);

console.log(hasExperiencedDriver);

const totalWalletBalance = registeredDrivers.reduce(
    (total, driver) => total + driver.wallet,
    0
);

console.log(totalWalletBalance);

const driverRecord = {
    name: "Tega",
    deliveries: 25,
    wallet: 37500
};

const { name, deliveries, wallet } = driverRecord;

console.log(name);
console.log(deliveries);
console.log(wallet);

const {wallet : pureWallet} = driverRecord
console.log(pureWallet)

const {bonus = 3000} = driverRecord
console.log(bonus);

const driverProfile = {
    name: "Tega",
    deliveries: 25,

    payment: {
        wallet: 37500,
        bonus: 5000,
        fuel: 1000
    }
};

console.log(driverProfile);

