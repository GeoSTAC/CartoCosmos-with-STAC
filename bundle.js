/*! For license information please see bundle.js.LICENSE.txt */
  0% {
    transform: scale(0);
    opacity: 0.1;
  }

  100% {
    transform: scale(1);
    opacity: 0.3;
  }
`)),ln=Je(nn||(nn=an`
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
`)),un=Je(rn||(rn=an`
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(0.92);
  }

  100% {
    transform: scale(1);
  }
`)),cn=(0,g.ZP)("span",{name:"MuiTouchRipple",slot:"Root"})({overflow:"hidden",pointerEvents:"none",position:"absolute",zIndex:0,top:0,right:0,bottom:0,left:0,borderRadius:"inherit"}),hn=(0,g.ZP)((function(e){const{className:n,classes:r,pulsate:i=!1,rippleX:o,rippleY:a,rippleSize:s,in:l,onExited:c,timeout:h}=e,[d,f]=t.useState(!1),p=(0,u.Z)(n,r.ripple,r.rippleVisible,i&&r.ripplePulsate),m={width:s,height:s,top:-s/2+a,left:-s/2+o},g=(0,u.Z)(r.child,d&&r.childLeaving,i&&r.childPulsate);return l||d||f(!0),t.useEffect((()=>{if(!l&&null!=c){const t=setTimeout(c,h);return()=>{clearTimeout(t)}}}),[c,l,h]),(0,A.jsx)("span",{className:p,style:m,children:(0,A.jsx)("span",{className:g})})}),{name:"MuiTouchRipple",slot:"Ripple"})(on||(on=an`
  opacity: 0;
  position: absolute;

  &.${0} {
    opacity: 0.3;
    transform: scale(1);
    animation-name: ${0};
    animation-duration: ${0}ms;
    animation-timing-function: ${0};
  }

  &.${0} {
    animation-duration: ${0}ms;
  }

  & .${0} {
    opacity: 1;
    display: block;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-color: currentColor;
  }

  & .${0} {
    opacity: 0;
    animation-name: ${0};
    animation-duration: ${0}ms;
    animation-timing-function: ${0};
  }

  & .${0} {
    position: absolute;
    /* @noflip */
    left: 0px;
    top: 0;
    animation-name: ${0};
    animation-duration: 2500ms;
    animation-timing-function: ${0};
    animation-iteration-count: infinite;
    animation-delay: 200ms;
  }
//# sourceMappingURL=bundle.js.map