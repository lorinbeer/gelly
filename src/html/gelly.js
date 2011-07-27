//==========================================================================================================================
/*    Gelly Javascript API
 *
 */
//==========================================================================================================================
/*  TODO
 *    EFFECTS
 *    CALLBACK MESSAGE
 *    FORMS
 *    UPDATE POS
 */
//==========================================================================================================================

//==========================================================================================================================
/*
 * send a message string to core
 *
 */
var dispatchmessage = function(message) {
    try{ 
        window.externalHost.postMessage( message, "about:blank" );
    }
    catch(e) {
        console.log( "postMessage: "+ message );
    }
}
//==========================================================================================================================
/*
 *  format a message for the game engine
 *
 *  @params target:
 *  @param request:
 *  @param kwargs: list of key value pairs as a list eg [ke1,va1,ke2,va2,ke3,va3...], an odd number of elements in the list
 *                 will generate 'undefined' as the value of the last key element. Strings only.
 */
var formatgemessage = function(target,request,kwargs) {
    //"type=gemessage
    var message = 'target='+target+';'+'request='+request+';';
    var arg;
    var next='{';
    while(arg=kwargs.shift()) {
        message += next+'"'+arg+'":"'+kwargs.shift()+'"';
        next=',';
    }
    return message+='}';
}
//==========================================================================================================================


//==========================================================================================================================
function GellyButton(id) {
  //look up dbid in db to get all image threads
    this.imgDown    = "/home/lorin/projects/gelly/art/ui/enchant-blue-3.png"
    this.imgDefault = "/home/lorin/projects/gelly/art/ui/enchant-blue-1.png"
    this.imgActive  = "/home/lorin/projects/gelly/art/ui/enchant-blue-2.png"
    this.imgBorder  = "/home/lorin/projects/gelly/art/ui/frame-9-red.png";
    this.id = id;
    this.active = 0;
    var self = this;
    $('#'+this.id).children().each( 
        function() { 
            if( $(this).hasClass('gelly-button-border')  ) {
                $(this).attr('src',self.imgBorder);
                self.border = $(this);
	    }
            else if( $(this).hasClass('gelly-button-icon') ) {
                $(this).attr('src',self.imgDefault);
                self.icon = $(this);
	    }     
    });
    //======================================================================================================================
    /*
     * default mouse event handlers, used if none are specified as arguments to the constructor
     *
     */
    $('#'+this.id).mouseenter( function(event) {
        self.icon.attr('src',self.imgActive);
    });
    $('#'+this.id).mouseout( function(event) {
        self.icon.attr('src',self.imgDefault);
    });
    $('#'+this.id).mousedown( function(event) {
        self.icon.attr('src',self.imgDown);
    });
    $('#'+this.id).mouseup( function(event) {
        self.icon.attr('src',self.imgActive);
        dispatchmessage( formatgemessage('character','queueskill',['slot',self.id]) );
    });			 
}
//==========================================================================================================================
GellyButton.prototype.seticons = function(images) {
    self.imgDown = images.imgDown;
    self.imgDefault = images.imgDefault;
    self.imgActive = images.imgActive;
    self.imgBorder = images.imgBorder;
}
//==========================================================================================================================

//==========================================================================================================================
//==========================================================================================================================

//==========================================================================================================================
/*
 * a container for other widgets
 *   
 * @param id:
 * @param menuid:
 *
 */
function GellyPanel(id,menuid) {
    this.id = '#'+id;
    this.menu = new GellyContextMenu(menuid,this,this);  
    this.buttons = new Object;
    this.activeButton = false;
    this.readChildren();
    var self = this;

    //======================================================================================================================
    $(this.id).mouseup( function(event) {
        if(event.button!=0) return;
        if( $(event.target).parent().hasClass('gelly-button') ) {
            var active = $(event.target).parent().attr('id');
            self.activeButton = self.buttons[active];
            self.menu.open( event.target );
	}
    });
    //======================================================================================================================
    $(this.id).mouseout( function(event) {
        if( $(event.target).attr('id') == $(self.id).attr('id')  ){
            self.menu.close();
	}
    });
    //======================================================================================================================
}
//==========================================================================================================================
/*
 * read and set any child elements GellyPanel recognizes (eg buttons) already present in the DOM
 *  if you want to add new children, use registerChildren
 */
GellyPanel.prototype.readChildren = function() {
    var panel = this;
    $(this.id).children().each( function() {
      var childid = $(this).attr('id');
      panel.buttons[childid] = new GellyButton( childid );
    });
}
//==========================================================================================================================
GellyPanel.prototype.registerChildren = function(children,overwrite){
  if(overwrite){
    this.clearChildren();
  }
}
//==========================================================================================================================
GellyPanel.prototype.clearChildren = function() {
}
//==========================================================================================================================
//==========================================================================================================================

//==========================================================================================================================
/*
 *  gelly panel's mouse out handler, used to shut down any open context menus
 *
 */
GellyPanel.prototype.onMouseOut = function(event) {
    var self = allPanels[ event.currentTarget.id ];
    var original = event.originalEvent.explicitOriginalTarget;
    if( ! $(original).hasClass('gelly-button') && ! $(original).hasClass('gelly-panel') ){
      $(self.menuid).hide();    
    }
}
//==========================================================================================================================

//==========================================================================================================================
//==========================================================================================================================

//==========================================================================================================================

//==========================================================================================================================
/*  
 *
 *
 */
//==========================================================================================================================
function GellyContextMenu(id,parent,panel) {
    this.menuitems = new Object();
    $('#'+id).hide();
    this.on = false;
    this.id = '#'+id;
    this.parent = parent;
    this.basepanel = panel;
    this.anchor = false;
    this.child = new Object;
    this.currentChild=false;

    var self = this;
    var _parent = parent;
    var msg = msg;
    //======================================================================================================================
    /*
     *  mousedown handler, responsible for handling all mousedown events for child menu items
     */
    $("#"+id).mousedown( function(event) {
        if ($(event.target).attr("action") == "open") {  
            var target = $(event.target).attr("target"); //construct our selector string
            if( self.currentChild ) {
                self.currentChild.close();
                self.currentChild=false;
	    }
            if( ! self.child.hasOwnProperty(target) ) {
                self.child[target] = new GellyContextMenu(target,self,self.basepanel);
	    }
            self.child[target].open(self.id);
            self.currentChild = self.child[target];
            $(self.child[target].id).position({ my: "left", at: "right", of: $(self.id), offset: "0 0", collision: "none"});
        }
        else if ( $(event.target).attr("action") == "message" ) {
            
            var value = '{'+$(event.target).attr('value')+','+
                            "'slot':"+ "'"+self.basepanel.activeButton.id + "'"+
                        '}';
            var msg = "target="   + $(event.target).attr('target')+";"
                      +"request=" + $(event.target).attr('request')+";"
                      + value;
            try {
                window.externalHost.postMessage( msg, "about:none" );
            }
            catch(e) {
	        console.log( "postMessage: "+ msg );
	    }
        }
    });
    //======================================================================================================================
    this.open = function(anchor) {
        self.on = true;
        self.anchor = anchor;
        $(self.id).show();
        $(self.id).position({my:"left",at:"right",of:$(anchor),offset:"0 0",collision:"none" });
	$(self.id).show( 'drop', {direction:'left'}, 500 );
        if(self.currentChild){
            self.currentChild.close();
            self.currentChild = false;
	}
    }
    //======================================================================================================================
    this.close = function() {
        if( self.on ) {
        self.on = false;
        if(self.currentChild){
            self.currentChild.close();
            self.currentChild = false;
	}
            console.log( self.id );
	    $(self.id).hide( 'drop', {direction:'right'}, 500 );
	}
    }
    //======================================================================================================================
}
//==========================================================================================================================
//==========================================================================================================================
/*
 *  GellyContextMenu.populate
 *    populate the context menu with the provided data
 */
GellyContextMenu.prototype.populate  = function(data) {
    var msg = "Context Menu Message";
    try {
	window.externalHost.postMessage( msg, queryURI );
    }
    catch(e) {
	console.log( "postMessage: "+ msg + " Target: " + queryURI );
    } 
}
//==========================================================================================================================
//==========================================================================================================================