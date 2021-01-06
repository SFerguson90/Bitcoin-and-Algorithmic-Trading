
import React, { useState, useEffect } from "react";
import FormControl from '@material-ui/core/FormControl';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import getWeb3 from "./utils/getWeb3";
import FactoryContract from "./contracts/FundraiserFactory.json";
import Web3 from 'web3'

const useStyles = makeStyles(theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
  },
  dense: {
    marginTop: theme.spacing(2),
  },
  menu: {
    width: 200,
  },
}));

const NewFundraiser = () => {
const [labelWidth, setLabelWidth] = React.useState(0);
const labelRef = React.useRef(null);
const classes = useStyles();
const [ web3, setWeb3 ] = useState(null)

useEffect(() => {
  const init = async() => {
    try {
      const web3 = await getWeb3();
      const networkId = await web3.eth.net.getId();
      const deployedNetwork = FactoryContract.networks[networkId];
      const accounts = await web3.eth.getAccounts();
      const instance = new web3.eth.Contract(
        FactoryContract.abi,
        deployedNetwork && deployedNetwork.address,
      );

      setWeb3(web3)
      setContract(instance)
      setAccounts(accounts)

    } catch(error) {
      alert(
        `Failed to load web3, accounts, or contract. Check console for details.`,
      );
      console.error(error);
    }
  }
  init();
}, []);

const [ name, setFundraiserName ] = useState(null)
const [ website, setFundraiserWebsite ] = useState(null)
const [ description, setFundraiserDescription ] = useState(null)
const [ image, setImage ] = useState(null)
const [ address, setAddress ] = useState(null)
const [ contract, setContract] = useState(null)
const [ accounts, setAccounts ] = useState(null)

const handleSubmit = async () => {
  const imageURL = image
  const url = website
  const beneficiary = address
  const currentUser = await web3.currentProvider.selectedAddress

  const transaction = await contract.methods.createFundraiser(
    name,
    url,
    imageURL,
    description,
    beneficiary
  ).send({ from: accounts[0] })

  alert('Successfully created fundraiser')
}

  return (
    <div className="new-client-information">
      <h1>New Client Information</h1>

      <label>First Name</label>
      <TextField
        id="outlined-bare"
        className={classes.textField}
        placeholder="First Name"
        margin="normal"
        onChange={(e) => setFundraiserName(e.target.value)}
        variant="outlined"
        inputProps={{ 'aria-label': 'bare' }}
      />

      <label>Last Name</label>
      <TextField
        id="outlined-bare"
        className={classes.textField}
        placeholder="Last Name"
        margin="normal"
        onChange={(e) => setFundraiserWebsite(e.target.value)}
        variant="outlined"
        inputProps={{ 'aria-label': 'bare' }}
      />

      <label>Current Address</label>
      <TextField
        id="outlined-bare"
        className={classes.textField}
        placeholder="Current Address"
        margin="normal"
        onChange={(e) => setFundraiserDescription(e.target.value)}
        variant="outlined"
        inputProps={{ 'aria-label': 'bare' }}
      />

      <label>Identifying Image</label>
      <TextField
        id="outlined-bare"
        className={classes.textField}
        placeholder="Drivers License/Passport/Green Card"
        margin="normal"
        onChange={(e) => setImage(e.target.value)}
        variant="outlined"
        inputProps={{ 'aria-label': 'bare' }}
      />

      <label>Wallet Address</label>
      <TextField
        id="outlined-bare"
        className={classes.textField}
        placeholder="Ethereum Wallet Address"
        margin="normal"
        onChange={(e) => setAddress(e.target.value)}
        variant="outlined"
        inputProps={{ 'aria-label': 'bare' }}
      />

      <Button
        onClick={handleSubmit}
        variant="contained"
        className={classes.button}>
        Enroll
      </Button>
    </div>
  )
}


export default NewFundraiser;
