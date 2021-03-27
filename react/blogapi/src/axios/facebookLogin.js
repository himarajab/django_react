import axios from 'axios';


const facebookLogin = (accesstoken) =>{
  console.log(accesstoken);
  axios.post('http://127.0.0.1:8000/auth/convert-token',{
    token:accesstoken,
    backend:'facebook',
    grant_type:'convert_token',
    client_id:'v3BT25VprgZS0HJvOvsg4bxB4OBNmbPBPqfctR5k',
    client_secret:'N6fi7auxhbb6ga6WjrCY4uljXzxe73DBuU657oe3L15nTUH05oB1e6KlE8mJSAl1QzM88KQqp2BUGsDBgDkA2MS6t9klEyPNNnzHTIrztNIpHmLzKksypUe51vLXiY8G',
  })
  .then((res) =>{
    localStorage.setItem('access_token',res.data.access_token);
		localStorage.setItem('refresh_token',res.data.refresh_token);
  });
};

export default facebookLogin;
