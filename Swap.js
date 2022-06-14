const serverUrl =  //Server url from moralis.io
const appId =   //Application id from moralis.io

let tokens;
let toaddress,fromaddress,qoutes,walletaddress, fromsympol, inamount, tosympol, algo_type,from_decimals ,f,to;
var i;
document.getElementById('logout_button').style.visibility = 'hidden';


async function Init() {
  await Moralis.start({ serverUrl, appId });
  await Moralis.enableWeb3();
  const result = await Moralis.Plugins.oneInch.getSupportedTokens({
    chain: "bsc", 
  });
  tokens = result.tokens;
  console.log(tokens)
  await ListAvailableTokens();
  currentUser = Moralis.User.current();
  
  document.getElementById("Run_button").disabled = false;
}

async function approveFunctionForFirstToken() {

  let fromTokenAddress = fromaddress;
  const Web3API = [
    {
      constant: false,
      inputs: [
        { internalType: "address", name: "spender", type: "address" },
        { internalType: "uint256", name: "amount", type: "uint256" }
      ],
      name: "approve",
      outputs: [{ internalType: "bool", name: "", type: "bool" }],
      payable: false,
      stateMutability: "nonpayable",
      type: "function"
    }
  ];

  const approve = {
    contractAddress: fromTokenAddress,
    functionName: "approve",
    abi: Web3API,
    params: {
      spender: "0x642ca54373E44450bC79F4239b914711D70b3F86",
      amount: "0xffffffffffffffffffffffffffffffff"
    }
  };

  const transaction = await Moralis.executeFunction(approve);
  console.log(transaction.hash);
  console.log(transaction);
  await transaction.wait();
}

async function approveFunctionForSecoundToken() { 

  let toTokenAddress = toaddress;
  const Web3API = [
    {
      constant: false,
      inputs: [
        { internalType: "address", name: "spender", type: "address" },
        { internalType: "uint256", name: "amount", type: "uint256" }
      ],
      name: "approve",
      outputs: [{ internalType: "bool", name: "", type: "bool" }],
      payable: false,
      stateMutability: "nonpayable",
      type: "function"
    }
  ];

  const approve = {
    contractAddress: toTokenAddress,
    functionName: "approve",
    abi: Web3API,
    params: {
      spender: "0x642ca54373E44450bC79F4239b914711D70b3F86",
      amount: "0xffffffffffffffffffffffffffffffff"
    }
  };

  const transaction = await Moralis.executeFunction(approve);
  console.log(transaction.hash);
  console.log(transaction);
  await transaction.wait();
}
 
async function approveTheBot() { approveFunction();
  approveFunctionForRevers();
}
 async function ListAvailableTokens() {
  for (const address in tokens) {
    let token = tokens[address];

    const fromcontainer =document.getElementById('fromtokens-dropdown');
    fromcontainer.innerHTML += `<button type="button" onclick="SelectToken('1','${token.address}', '${token.symbol}', '${token.decimals}', '${token.logoURI}')" class="tokens-links" id="${token.name}">
    <img class = "token_list_img" src="${token.logoURI}" />
    ${token.symbol}
    </button>
    `;
    const tocontainer  =document.getElementById('totokens-dropdown');
    tocontainer.innerHTML += `<button type="button" onclick="SelectToken('2','${token.address}', '${token.symbol}', 0, '${token.logoURI}')" class="tokens-links" id="${token.name}">
    <img class = "token_list_img" src="${token.logoURI}" />
    ${token.symbol}
    </button>
    `;  }
};

function SelectToken(id,address,token, decimals,logo) {
  if (id==1){
    console.log("fromtoken",address);
    fromaddress=address;
    fromsympol=token;
    from_decimals=decimals;
    const fh = document.getElementById('fortextmeny');
    token=" "+token;
    fh.innerHTML='<img class = "token_list_img" src='+logo+' /><h6 id="fortextmeny" > '+token+'</h6>';
    document.getElementById('fromtokens-dropdown').style.display = 'none'
    //fromtoggle('fromtokens-dropdown')

  }
  else if (id==2){
    console.log(id,address,token, decimals,logo);
    console.log("to token",address);
    toaddress=address;
    tosympol=token;
    const th = document.getElementById('totextmeny');
    th.innerHTML='<img class = "token_list_img" src='+logo+' /><h6 id="totextmeny"> '+token+'</h6>';
    document.getElementById('totokens-dropdown').style.display = 'none'
    //totoggle('totokens-dropdown')
  }
}

async function Login(){
  console.log("login clicked");
  var user = await Moralis.Web3.authenticate();
  if(user){
    user.save();
    userAddress=Moralis.User.current().get("ethAddress");
    action1();
    alert("you logged in")
  }
  else{
    console.log("Error")
  }
}

async function LogOut() {
  await Moralis.User.logOut();
  console.log("logged out");
}
var hidden = false;
function action1() {
        document.getElementById('login_button').style.visibility = 'hidden';
   
        document.getElementById('logout_button').style.visibility = 'visible';    
}

function action2() {
        document.getElementById('logout_button').style.visibility = 'hidden';

        document.getElementById('login_button').style.visibility = 'visible';
  
}
function loginbtn(){
  Login();
}
function logoutbtn(){
  LogOut();
  action2();
  alert("you logged out")
}

Init();

document.getElementById("login_button").onclick = loginbtn;
document.getElementById("logout_button").onclick = logoutbtn;
document.getElementById("Run_button").onclick = run_the_bot;
document.getElementById("approve").onclick = approveTheBot;



function CheckInfo(){
let amount = Number(document.getElementById("from_amount").value * 10 ** from_decimals); 
inamount = amount / 1000000000000000000; 
algo_type=document.getElementById("lang").value

if (fromaddress == null || toaddress==null ||userAddress == null ||inamount == null 
    ){
  alert("Please make sure that you entered all the values, and try again")
  }
else{
     alert("the bot started")
    }
}

function FetchPostMessage(){
  fetch('http://127.0.0.1:5001/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json' 
    },
    body:  JSON.stringify({ from:fromaddress ,till:toaddress ,user_address:userAddress,sympol:fromsympol,
       inamount: inamount , tosympol: tosympol, strategi:algo_type })
  })  
}

function run_the_bot(){
  console.log("Bot started")
  CheckInfo()
  FetchPostMessage()
}

function fromtoggle(el) {
  var tag=document.getElementById(el);
  tag.style.display = tag.style.display === 'block' ? 'none' : 'block';
}

function totoggle(el) {
  var tag=document.getElementById(el);
  tag.style.display = tag.style.display === 'block' ? 'none' : 'block';
}