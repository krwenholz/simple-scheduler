/** @jsx React.DOM */

var DynamicSearch = React.createClass({

  // sets initial state
  getInitialState: function(){
    return { searchString: '' };
  },

  // sets state, triggers render method
  handleChange: function(event){
    // grab value form input box
    this.setState({searchString:event.target.value});
    console.log('Search string updated with ' + event.target.value);
  },

  render: function() {

    var client_names = this.props.items;
    var searchString = this.state.searchString.trim().toLowerCase();

    // filter client_names by value from input box
    if(searchString.length > 0){
      client_names = client_names.filter(function(name){
        return name.name.toLowerCase().match( searchString );
      });
    }

    return (
      <div>
        <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Find yourself" />
        <ul>
          { client_names.map(function(name){ return <li>{name.name} </li> }) }
        </ul>
      </div>
    )
  }

});

// list of clients, defined with JavaScript object literals
var client_names = [
    {"name": "Jerrell"},
    {"name": "Conchita"},
    {"name": "Malinda"},
    {"name": "Cammie"},
    {"name": "Clemmie"},
    {"name": "Lane"},
    {"name": "Irmgard"},
    {"name": "Coy"},
    {"name": "Nickole"},
    {"name": "Tawanna"},
    {"name": "Buddy"},
    {"name": "Shirley"},
    {"name": "Bradley"},
    {"name": "Samantha"},
    {"name": "Reba"},
    {"name": "Lemuel"},
    {"name": "Blossom"},
    {"name": "Raelene"},
    {"name": "Delmar"},
    {"name": "Pearly"},
    {"name": "Myles"},
    {"name": "Amado"},
    {"name": "Danyell"},
    {"name": "Monte"},
    {"name": "Crissy"},
    {"name": "Jimmy"},
    {"name": "Scotty"},
    {"name": "Launa"},
    {"name": "Malissa"},
    {"name": "Verlene"},
    {"name": "Lavera"},
    {"name": "Estell"},
    {"name": "Torie"},
    {"name": "Ronny"},
    {"name": "Teisha"},
    {"name": "Clint"},
    {"name": "Jaqueline"},
    {"name": "Natalia"},
    {"name": "Hope"},
    {"name": "Toshiko"},
    {"name": "Leonardo"},
    {"name": "Ai"},
    {"name": "Corazon"},
    {"name": "Hermelinda"},
    {"name": "Renetta"},
    {"name": "Joline"},
    {"name": "Buena"},
    {"name": "Stan"},
    {"name": "Olympia"},
    {"name": "Gabriele"},
    {"name": "Tony"}, 
    {"name": "Sonya"}, 
    {"name": "Johnny"}, 
    {"name": "Melinda"},
    {"name": "Jack"}, 
    {"name": "Jona"}, 
];

React.render(
    <DynamicSearch items={ client_names } />,
    document.getElementById('main'));

