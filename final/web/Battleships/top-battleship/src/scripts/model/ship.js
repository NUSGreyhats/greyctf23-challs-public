const Ship = (length, name = 'ship') => {
  const proto = {
    getHit() {
      --this.hitPoints;

      if (this.hitPoints <= 0) {
        this.isSunk = true;
      }
    },
    rotate() {
      this.orientation =
        this.orientation === 'vertical' ? 'horizontal' : 'vertical';
    },
  };

  const props = {
    name,
    length,
    hitPoints: length,
    orientation: 'vertical',
    isOnBoard: false,
    isSunk: false,
  };

  return Object.assign(Object.create(proto), props);
};

export default Ship;
